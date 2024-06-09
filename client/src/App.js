import React, { useState, useEffect } from 'react'
import 'semantic-ui-css/semantic.min.css'
import './App.css'
import { Progress, TabPane, Tab } from 'semantic-ui-react'

function App() {

  const [reference, setReference] = useState('')
  const [result, setResult] = useState('')

  const [selectedLanguage, setSelectedLanguage] = useState('')
  const [resultLanguage, setResultLanguage] = useState('Russian')

  const [errorMessage, setErrorMessage] = useState('')

  const [isLoading, setIsLoading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [sendButtonState, setSendButtonState] = useState(false)

  const [showAdditionalField, setShowAdditionalField] = useState(false)
  const [additionalResult, setAdditionalResult] = useState('')

  // call an api to detect language
  const languageDetection = () => {
    return fetch("/detect_language", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ reference: reference })
    })
    .then(response => response.json())
    .then(data => {
      if (data.language !== "Russian" && data.language !== "Kazakh" 
      && data.language !== "English") {
        return ""
      }
      return data.language
    })
    .catch(error => {
      console.error('error:', error)
      return ""
    })
  }

  // send button function
  const handleClick = async () => {

    setSelectedLanguage("")
    setResult("")
    setAdditionalResult("")
    setShowAdditionalField(false)
    setSendButtonState(true)

    if (reference === "") {
      setErrorMessage("input text can't be empty.")
      return
    }
    
    setIsLoading(true)
    setProgress(25)

    const detectedLanguage = await languageDetection()

    if (detectedLanguage !== "Russian" && detectedLanguage !== "Kazakh" 
    && detectedLanguage !== "English") {
      setErrorMessage("input text language must be Kazakh, Russian or English.")
      setIsLoading(false)
      return
    }

    setSelectedLanguage(detectedLanguage)

    if (selectedLanguage == 'Russian' || selectedLanguage == 'English' || 
    selectedLanguage == 'Kazakh') {
      if (selectedLanguage != resultLanguage) {
        setShowAdditionalField(true)
      } else {      
        setShowAdditionalField(false)
      }
    }

    setErrorMessage("")
    setProgress(50)
    
    const updateProgress = (start, end) => {
      return new Promise((resolve) => {
        const duration = 10000; 
        const stepTime = 100; 
        const steps = (end - start) / (duration / stepTime);

        let currentProgress = start;
        const interval = setInterval(() => {
          currentProgress += steps;
          setProgress(currentProgress);

          if (currentProgress >= end) {
            clearInterval(interval);
            resolve();
          }
        }, stepTime);
      });
    };

    updateProgress(50, 100) 

    fetch("/get_reference", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ reference: reference, resultLanguage: resultLanguage })
    })
    .then(
      response => response.json()
    )
    .then(data => {
      setResult(data.result)
      setAdditionalResult(data.translated_reference)
      setProgress(100)
      setIsLoading(false)
      setSendButtonState(false)
    })
    .catch(error => {
      console.error('error:', error)
      setIsLoading(false)
      setProgress(0)
    });
  };

  // input field header logic
  let languageMessage;
  if (selectedLanguage) {
    languageMessage = selectedLanguage 
  } else {
    languageMessage = "enter any text in the field"
  }

  // tabs for different languages
  const additionalPanes = [
    { menuItem: 'alternative meaning', render: () => <TabPane>
      <div className="ui form">
        <textarea value = { result } placeholder = "alternative meaning" readOnly></textarea>          
      </div>
    </TabPane> },
    { menuItem: 'direct translation', render: () => <TabPane>
      <div className="ui form">
        <textarea value = { additionalResult } placeholder = "translation" readOnly></textarea>          
      </div>
    </TabPane> }
  ]

  //tab for same languages
  const panes = [
    { menuItem: 'alternative meaning', render: () => <TabPane>
      <div className="ui form">
        <textarea value = { result } placeholder = "alternative meaning" readOnly></textarea>          
      </div>
    </TabPane> }
  ]

  return (
    <div className="ui center aligned container">

      {errorMessage && (
        <div className="ui negative message">
          <i className="close icon" onClick={ () => setErrorMessage('') }></i>
          <div className = "header">
            error
          </div>
          <p>{ errorMessage }</p>
        </div>
      )}

      <div className="ui visible message">
        <p>{ languageMessage }</p>
      </div>

      <div className="ui form">
        <textarea 
          value = { reference }
          onChange = {(e) => setReference(e.target.value)}
          placeholder="enter a text" 
          rows="5" 
        ></textarea>
      </div>
      <br />
      
      <div>
        <button 
          className="ui button" 
          onClick = { handleClick } 
          id="send.button"
          disabled={ sendButtonState }
        >send</button>
      </div> 

      {isLoading && (
        <Progress percent={progress} indicating />
      )}

      <div className = "ui visible message">
        <p>choose the result language</p>
        <select 
          className = "ui search dropdown"
          value = { resultLanguage }
          onChange = { (e) => setResultLanguage(e.target.value) }
        >
          <option value="Russian">Russian</option>
          <option value="English">English</option>
          <option value="Kazakh">Kazakh</option>        
        </select>
      </div>

      <div>
        {showAdditionalField && (
          <Tab panes={additionalPanes} />
        )}
        {!showAdditionalField && (
          <Tab panes={panes} />
        )}
      </div>

    </div>
  )
}

export default App

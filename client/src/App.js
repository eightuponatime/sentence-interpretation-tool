import React, { useState, useEffect } from 'react'
import 'semantic-ui-css/semantic.min.css'
import './App.css'
import { Progress, TabPane, Tab, Popup } from 'semantic-ui-react'
import AccordionComponent from './AccordionComponent'

function App() {

  const [reference, setReference] = useState('')
  const [result, setResult] = useState('')
  const [results, setResults] = useState([])

  // language of input text
  const [selectedLanguage, setSelectedLanguage] = useState('')
  // language from the radiobuttons
  const [resultLanguage, setResultLanguage] = useState('Russian');

  const [errorMessage, setErrorMessage] = useState('')

  const [isLoading, setIsLoading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [sendButtonState, setSendButtonState] = useState(false)

  const [showAdditionalField, setShowAdditionalField] = useState(false)
  const [additionalResult, setAdditionalResult] = useState('')

  // call an api to detect language
  const languageDetection = () => {
    return fetch("https://amd64flask-backend-r5vrjzoy5a-uc.a.run.app/detect_language", {
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
      setSendButtonState(false)
      return
    }
    
    setIsLoading(true)
    setProgress(25)

    const detectedLanguage = await languageDetection()

    if (detectedLanguage !== "Russian" && detectedLanguage !== "Kazakh" 
    && detectedLanguage !== "English") {
      setErrorMessage("input text language must be Kazakh, Russian or English.")
      setIsLoading(false)      
      setSendButtonState(false)
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

    fetch("https://amd64flask-backend-r5vrjzoy5a-uc.a.run.app/get_reference", {
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
      if(!data || !Array.isArray(data.results) || data.results.length === 0) {
        setErrorMessage("no results found")
        setIsLoading(false)
        setSendButtonState(false)
        return
      }
      setResult(data.result)
      setAdditionalResult(data.translated_reference)
      setResults(data.results)
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
    { menuItem: 'alternative meaning', render: () => <TabPane style={{ fontSize: 18 }}>
      <div className="ui form">
        <textarea value = { result } placeholder = "alternative meaning" readOnly></textarea>          
      </div>
    </TabPane> }
  ]

  // (language chooser) radio button value setter
  const handleRadioChange = ( value ) => {
    setResultLanguage(value);
  }

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

      <div className="ui visible message">
        <div className="radioGroup"> 
          <div className="radioButton">
            <input 
              type="radio" 
              value="Russian" 
              checked = { resultLanguage === "Russian"}
              onChange= { () => handleRadioChange("Russian")}
            />
            <label htmlFor="Russian" className="radioLabel">Russian</label>  
          </div>
          <div className="radioButton">
            <input 
              type="radio" 
              value="English" 
              checked = { resultLanguage === "English"}
              onChange= { () => handleRadioChange("English")}
            />
            <label htmlFor="English" className="radioLabel">English</label>  
          </div>
          <div className="radioButton">
            <input 
              type="radio" 
              value="Kazakh" 
              checked = { resultLanguage === "Kazakh"}
              onChange= { () => handleRadioChange("Kazakh")}
            />
            <label htmlFor="Kazakh" className="radioLabel">Kazakh</label>  
          </div>
        </div>
      </div>

      <br />

      <div>
        {showAdditionalField && (
          <Tab panes={additionalPanes} />
        )}
        {!showAdditionalField && (
          <Tab panes={panes} />
        )}
      </div>

      <br />
      {result && (
        <AccordionComponent data={results} result={result} />
      )}
    </div>
  )
}

export default App

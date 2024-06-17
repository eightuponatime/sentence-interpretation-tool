import React, { Component } from 'react';
import { Accordion, AccordionTitle, AccordionContent, Icon } from 'semantic-ui-react';

class AccordionComponent extends Component {
  state = { activeIndex: null };

  componentDidMount() {
    const { data } = this.props;
    const maxScore = Math.max(...data.map(item => item.score));
    const maxScoreIndex = data.findIndex(item => item.score === maxScore);

    this.setState({ activeIndex: maxScoreIndex });
  }

  handleClick = (e, titleProps) => {
    const { index } = titleProps;
    const { activeIndex } = this.state;
    const newIndex = activeIndex === index ? -1 : index;

    this.setState({ activeIndex: newIndex });
  };

  render() {
    const { activeIndex } = this.state;
    const { data, result } = this.props; 
    return (
      <Accordion fluid styled>
        {data.map((item, index) => (
          <React.Fragment key={index}>
            <AccordionTitle
              active={activeIndex === index}
              index={index}
              onClick={this.handleClick}
              style={{
                backgroundColor: '#303030', 
                color: item.candidate === result ? 'lightgreen' : 'lightpink' 
              }}
            >
              <Icon name="dropdown" />
              {item.candidate}
            </AccordionTitle>
            <AccordionContent active={activeIndex === index}>
              <p style={{ 
                backgroundColor: '#1e1e1e',
                color: 'white'
              }}>{item.score}</p>
            </AccordionContent>
          </React.Fragment>
        ))}
      </Accordion>
    );
  }
}

export default AccordionComponent;
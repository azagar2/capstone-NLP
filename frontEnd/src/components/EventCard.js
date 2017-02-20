import React, { Component } from 'react';
import '../styles/EventCard.css';

class EventCard extends Component {
  render() {
    return (
      <div className="card event-card">
        <div> {this.props.eventTitle} </div>
        <div> {this.props.eventDescription} </div>
        <div> {this.props.eventTags} </div>
      </div>
    );
  }
}

export default EventCard;

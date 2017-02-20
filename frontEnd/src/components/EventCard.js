import React, { Component } from 'react';
import '../styles/EventCard.css';

class EventCard extends Component {
  render() {
    return (
      <div className="card event-card">
        <div className="event-title"> {this.props.eventTitle} </div>
        <div className="event-description"> {this.props.eventDescription} </div>
        <div> {this.props.eventCategory} </div>
        <div> {this.props.eventLocation} </div>
      </div>
    );
  }
}

export default EventCard;

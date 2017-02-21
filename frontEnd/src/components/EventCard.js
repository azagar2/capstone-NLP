import React, { Component } from 'react';
import '../styles/EventCard.css';

class EventCard extends Component {
  render() {
    return (
      <div className="card event-card">
        <div className="event-title"> {this.props.eventTitle} </div>
        <div className="event-description"> {this.props.eventDescription} </div>
        <div className="event-category"> {this.props.eventCategory} </div>
        <div className="event-location"> {this.props.eventLocation} </div>
      </div>
    );
  }
}

export default EventCard;

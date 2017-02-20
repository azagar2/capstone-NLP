import React, { Component } from 'react';
import '../styles/RecommendEvents.css';

import UserCard from './UserCard';
import EventCard from './EventCard';

class RecommendEvents extends Component {
  render() {
    return (
      <div className="recommend-events-background">
        <h1 className='page-title'> Recommend Events </h1>
        <div className="recommend-events-container">
          <UserCard></UserCard>
          <div className="events-container">
            <EventCard></EventCard>
            <EventCard></EventCard>
            <EventCard></EventCard>
            <EventCard></EventCard>
          </div>
        </div>
      </div>
    );
  }
}

export default RecommendEvents;

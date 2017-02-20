import React, { Component } from 'react';
import '../styles/RecommendEvents.css';

import UserCard from './UserCard';
import EventCard from './EventCard';

class RecommendEvents extends Component {

recommendEvents(){
  alert("recommended");
}

  render() {
    return (
      <div className="recommend-events-background">
        <h1 className='page-title'> Recommend Events </h1>
        <div className="button-group">
          {/* TODO: drop down */}
          <div onClick={this.recommendEvents.bind(this)} className="button-pink"> Recommend </div>
        </div>

        {/* TODO: move this into a component */}
        <div className="recommend-events-container">
          <UserCard location="London, ON"></UserCard>
          <div className="events-container">
            <EventCard eventLocation="London, ON" eventTitle="Some Event" eventDescription="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum." eventCategory="Business"></EventCard>
            <EventCard eventLocation="London, ON" eventTitle="Some Event" eventDescription="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum." eventCategory="Business"></EventCard>
            <EventCard eventLocation="London, ON" eventTitle="Some Event" eventDescription="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum." eventCategory="Business"></EventCard>
            <EventCard eventLocation="London, ON" eventTitle="Some Event" eventDescription="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum." eventCategory="Business"></EventCard>
          </div>
        </div>

      </div>
    );
  }
}

export default RecommendEvents;

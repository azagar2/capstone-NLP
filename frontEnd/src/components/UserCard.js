import React, { Component } from 'react';
import '../styles/UserCard.css';

class UserCard extends Component {
  render() {
    // var img = require(`${this.props.img}`);
    // console.log(`${this.props.img}`);
    return (
      <div className="card user-card">
        <img src={ require('../images/ryan.jpg') } role="presentation" alt={this.props.name} className="circle-image"/>
        <hr className="horizontal-line"/>
        <div className="fakt"> {this.props.name} </div>
      </div>
    );
  }
}

export default UserCard;

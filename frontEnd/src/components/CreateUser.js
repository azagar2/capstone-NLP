import React, { Component } from 'react';
// import Bs, { Col } from 'react-bootstrap';
var Scroll  = require('react-scroll');

import '../styles/CreateUser.css';
import UserCard from './UserCard';

class CreateUser extends Component {

  scrollWin(){
    var scroll = Scroll.animateScroll;
    scroll.scrollTo(1400);
  }

  render() {
    return (
      <div className="create-user-background">
        <h1 className='page-title'> Create Users </h1>
        <div className="create-user-container">
          <UserCard img="../images/ryan.jpg" name="User 1"></UserCard>
          <br/>
          <div onClick={this.scrollWin.bind(this)} className="button-pink">Continue</div>
        </div>
      </div>
    );
  }
}

export default CreateUser;

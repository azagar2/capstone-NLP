import React, { Component } from 'react';
var Scroll  = require('react-scroll');

import '../styles/CreateUser.css';
import UserCard from './UserCard';
import AddFeature from './AddFeature';

class CreateUser extends Component {

  scrollWin(){
    var scroll = Scroll.animateScroll;
    scroll.scrollTo(window.innerHeight * 2);
  }

  addUser(){
    //open a modal to set location of user
    alert("user");
  }

  addEvent(){
    //open a modal to search db for events
    alert("event");
  }

  render() {
    return (
      <div className="create-user-background" >
        <div className="create-user-container">
          <h1 className='page-title'> Create Users </h1>

          <AddFeature type="user"></AddFeature>

          <div onClick={this.scrollWin.bind(this)} className="button-pink">
            Continue
          </div>

          {/* <div className="create-user-container">
            <UserCard img="../images/ryan.jpg" name="User 1" location="London, ON"/>
            <br/>
          </div> */}
        </div>
      </div>
    );
  }
}

export default CreateUser;

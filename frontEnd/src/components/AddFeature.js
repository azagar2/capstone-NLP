import React, { Component } from 'react';
import Modal from 'react-modal';
var Scroll  = require('react-scroll');

import '../styles/AddFeature.css';
import AddUserModal from './AddUserModal';

class AddFeature extends Component {

  scrollWin(){
    var scroll = Scroll.animateScroll;
    scroll.scrollTo(window.innerHeight * 2);
  }

  addUser(){
    //TODO: open a modal to set location of user
    // this.props
    alert("user");
  }

  addEvent(){
    //TODO: open a modal to search db for events
    alert("event");
  }

  render() {
    if(this.props.type === "user"){
      return (
        <div>
          <AddUserModal></AddUserModal>

          <div className="card add-user-card" onClick={this.addUser.bind(this)}>
            <div className="add-text">
              <span className="plus"> + </span> Add User
            </div>
          </div>
        </div>
      );
    } else {
      return (
        <div className="card add-event-card" onClick={this.addEvent.bind(this)}>
          <div className="add-text">
            <span className="plus"> + </span> Add Event
          </div>
        </div>
      );
    }
  }
}

export default AddFeature;

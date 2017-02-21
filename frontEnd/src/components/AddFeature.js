import React, { Component } from 'react';
import Modal from 'react-modal';
var Scroll  = require('react-scroll');

import '../styles/AddFeature.css';
// import AddUserModal from './AddUserModal';

class AddFeature extends Component {

  constructor(){
    super();
    this.state = {userOpen: false, eventUser: false};
  }

  scrollWin(){
    var scroll = Scroll.animateScroll;
    scroll.scrollTo(window.innerHeight * 2);
  }

  closeUserModal(){
    this.setState({userOpen: false});
  }

  addUser(){
    //TODO: open a modal to set location of user
    this.setState({userOpen: true});
  }

  closeEventModal(){
    this.setState({eventOpen: false});
  }

  addEvent(){
    //TODO: open a modal to search db for events
    this.setState({eventOpen: true});
  }

  render() {
    if(this.props.type === "user"){
      return (
        <div>

          <div className="card add-user-card" onClick={this.addUser.bind(this)}>
            <div className="add-text">
              <span className="plus"> + </span> Add User
            </div>
          </div>

          <div>
            <Modal isOpen={this.state.userOpen} onRequestClose={this.closeUserModal.bind(this)} closeTimeoutMS={0} contentLabel="Modal">
              <h1>User Modal Content</h1>
              <p>Etc.</p>
            </Modal>
          </div>

        </div>
      );
    } else {
      return (
        <div>
          <div className="card add-event-card" onClick={this.addEvent.bind(this)}>
            <div className="add-text">
              <span className="plus"> + </span> Add Event
            </div>
          </div>

          <div>
            <Modal isOpen={this.state.eventOpen} onRequestClose={this.closeEventModal.bind(this)} closeTimeoutMS={0} contentLabel="Modal">
              <h1>Event Modal Content</h1>
              <p>Etc.</p>
            </Modal>
          </div>

        </div>
      );
    }
  }
}

export default AddFeature;

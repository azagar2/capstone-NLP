import React, { Component } from 'react';
import Modal from 'react-modal';
var Scroll  = require('react-scroll');

// import '../styles/AddUserModel.css';

class AddUserModal extends Component {

  closeUserModal(){
    alert("closed");
  }

  render() {
    return(
      <div>
        <Modal isOpen={false} onRequestClose={"closeUserModal"} closeTimeoutMS={1000}>
          <h1>Modal Content</h1>
          <p>Etc.</p>
        </Modal>
      </div>
    );
  }
}

export default AddUserModal;

import React, { Component } from 'react';
import './styles/App.css';

import UserCard from './components/UserCard'
import Landing from './components/Landing'
import CreateUser from './components/CreateUser'
import RecommendEvents from './components/RecommendEvents' 

class App extends Component {
  constructor(props){
    super(props)
    this.state = {}
  }

  render() {
    return (
      <div>
        <Landing/>
        <CreateUser/>
        <RecommendEvents/>
      </div>
    );
  }
}

export default App;

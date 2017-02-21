import React, { Component } from 'react';
import './styles/App.css';

import Landing from './components/pages/Landing'
import CreateUser from './components/pages/CreateUser'
import RecommendEvents from './components/pages/RecommendEvents'

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

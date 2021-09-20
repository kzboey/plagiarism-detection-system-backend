import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import App from './App'
import MatchingReport from './layouts/MatchReport'
import NavBar from './components/NavBar'

export const Routing = () => {
    return(
      <Router>
        <NavBar title="Plagiarism Detection System"/>
        <Switch>
          <Route exact path="/home" component={App} />
          <Route path="/report" component={MatchingReport} />
        </Switch>
      </Router>
    )
  }
  
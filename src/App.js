import React, { Component, Fragment } from 'react';
import { BrowserRouter as Router, Route, Switch,Redirect } from 'react-router-dom';
import MatchingReport from './layouts/MatchReport'
import Login from './layouts/Login'
import MyTask from './layouts/MyTask'
import NavBar from './components/NavBar'

class App extends Component {
  
    constructor(props) {
      super(props)   
    }

    getNavBar = () => {
      if(this.props.location.pathname !== '/' || this.props.location.pathname !== '/login'){
        return <NavBar title="Plagiarism Detection System"/>
      }
    }

    render(){
      return (
        <div>
          <Router>
            <Switch>
              <Redirect exact from="/" to="/login" />
              <Route exact path="/login" component={Login} />
              <Fragment>
                <NavBar title="Plagiarism Detection System"/>
                <Route exact path="/home" component={MyTask} />
                <Route path="/report" component={MatchingReport} />
              </Fragment>
            </Switch>
          </Router>
        </div>
      )
    }  
}

export default App;

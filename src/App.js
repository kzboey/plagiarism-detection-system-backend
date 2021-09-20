import React, { Component } from 'react';
import './App.css';
import TaskLists from './layouts/MyTask/index'
import NavBar from './components/NavBar'

class App extends Component {					
    render(){
      return (
        <div>
            <TaskLists/>
        </div>
      )
    }  
}

export default App;

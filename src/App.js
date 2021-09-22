import React, { Component } from 'react';
import './App.css';
import TaskLists from './layouts/MyTask/index'
import Login from './layouts/Login/index'

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

import React, { Component } from 'react'
import {Container} from '@material-ui/core';
import DynamicTables from '../../components/DynamicTables'
import CustomButton from '../../components/CustomButton'

class TaskLists extends Component{
    constructor(props) {
        super(props) //since we are extending class Table so we have to use super in order to override Component class constructor
     }

     render(){
        return(
            <Container>
                <DynamicTables />
            </Container>
        )
     }
}

export default TaskLists
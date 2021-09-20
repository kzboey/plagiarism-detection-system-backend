import React, { Component } from 'react';
import {MATCHDATA } from '../resources/MatchData';
import '../styles/media.scss';
import {Container,Grid} from '@material-ui/core';

class DynamicBox extends Component{
    constructor(props) {    //improve pass table cell as table data through props
        super(props);
        this.state = {
            mdata : MATCHDATA
        }
    }

    render(){
        return(
            <Container>
                <span className="title" >Match Overview</span>
                {this.state.mdata.map((row,index) => (
                    <div className="match-table-background"> 
                        <div className="match-table-index">
                            {++index}
                        </div>
                        <div className="match-table-string">
                            <span>{row.string}</span>
                            <span>{row.sources}</span>
                        </div>
                        <div className="match-table-similiar">
                            <span >{row.similiarity}</span>
                        </div>
                    </div>                        
                ))}
            </Container>         
        )
    }
}
export default DynamicBox

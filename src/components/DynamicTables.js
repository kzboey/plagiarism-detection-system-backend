import React, { Component } from 'react';
import { ASSIGNMENTS } from '../resources/Assignments';
import {Button} from '@material-ui/core';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import InfoIcon from '@material-ui/icons/Info';
import GetAppIcon from '@material-ui/icons/GetApp';
import '../styles/media.scss';
import {Redirect} from 'react-router-dom';

class DynamicTables extends Component{
    constructor(props) {    //improve pass table cell as table data through props
        super(props);
        this.state = {
            assignments : ASSIGNMENTS
        }
    }

    renderTableData(){
        return(
            <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Assignment</TableCell>
                  <TableCell align="right">Info</TableCell>
                  <TableCell align="right">Dates</TableCell>
                  <TableCell align="right">Similiarity</TableCell>
                  <TableCell align="right">Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {this.state.assignments.map((row) => (
                  <TableRow key={row.title}>
                    <TableCell component="th" scope="row">
                      {row.title}
                    </TableCell>
                    <TableCell align="right"><InfoIcon/></TableCell>
                    <TableCell align="right">
                        <span>start : {row.dates.start}</span>
                        <span>due : {row.dates.due}</span>
                        <span>submitted : {row.dates.submitted}</span>
                    </TableCell>
                    <TableCell align="right">{row.similiarity}</TableCell>
                    <TableCell align="right">
                        <Button color="primary"> Upload </Button>
                        <Button color="primary" onClick={this.viewReport}> View </Button>
                        <GetAppIcon/>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )
    }

    render(){
        return(
            <div>
            <h2>Submissions:</h2>
                <div>
                    {this.renderTableData()}
                </div>
            </div>
        )
    }

    viewReport = () => {
        return  <Redirect  to="/report" />
    }
}

export default DynamicTables


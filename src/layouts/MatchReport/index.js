import React, { Component } from 'react'
import sample2 from '../../resources/sample2.png'; // Tell webpack this JS file uses this image
import sample3 from '../../resources/sample3.jpeg'; // Tell webpack this JS file uses this image
import {Container,Grid} from '@material-ui/core';
import DynamicBox from '../../components/DynamicBox' 
import { withStyles } from '@material-ui/core/styles';
import '../../styles/media.scss';
import NavBar from '../../components/NavBar'

const useStyles = theme => ({
    root: {
      flexGrow: 1,
      textAlign : 'left'
    },
    paper: {
      padding: theme.spacing(1),
      textAlign: 'center',
      color: 'red'
    },
  });

class MatchingReport extends Component{
    
    constructor(props) {
        super(props) //since we are extending class Table so we have to use super in order to override Component class constructor
     }
     
     render(){
        const { classes } = this.props;
        return(
            <div>
                <Container className={classes.root}>   
                    <Grid container spacing={3}>
                        <Grid item xs={7}>
                            <img src={sample3} />
                            <img src={sample2} />
                        </Grid>
                        <Grid item xs={5}>
                            <DynamicBox />
                        </Grid>
                    </Grid>
                </Container>`  
            </div>       
        )
     }
}

export default withStyles(useStyles) (MatchingReport)
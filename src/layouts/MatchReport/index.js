import React, { Component } from 'react'
import sample2 from '../../resources/sample2.png'; // Tell webpack this JS file uses this image
import sample3 from '../../resources/sample3.jpeg'; // Tell webpack this JS file uses this image
import {Container,Grid,Box} from '@material-ui/core';
import DynamicBox from '../../components/DynamicBox'; 
import { withStyles } from '@material-ui/core/styles';
import Image from 'material-ui-image'
import '../../styles/media.scss';

const useStyles = theme => ({
    root: {
      flexGrow: 1,
      textAlign : 'left'
    }
  });

class MatchingReport extends Component{
    
    constructor(props) {
        super(props) //since we are extending class Table so we have to use super in order to override Component class constructor
     }
     
     render(){
        const { classes } = this.props;
        return(
            <Box className="whole-container">
                <Container className={classes.root}>   
                    <Grid container spacing={3}>
                        <Grid item xs={7} spacing={2}>
                            <Image src={sample3}/>
                        </Grid>
                        <Grid item xs={5}>
                            <DynamicBox />
                        </Grid>
                    </Grid>
                </Container>`  
            </Box>       
        )
     }
}

export default withStyles(useStyles) (MatchingReport)
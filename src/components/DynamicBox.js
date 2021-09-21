import React, { Component } from 'react';
import {MATCHDATA } from '../resources/MatchData';
import '../styles/media.scss';
import {Container,Typography,Divider,Box} from '@material-ui/core';
import { List, ListItem, ListItemText } from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';

const useStyles = theme => ({
    matchlist: {
        border : '1px solid #06080a' ,
        padding : '0px'
    },
    matchListItem: {
        color : 'black'
    },
    listIndex: {
        padding : '10px'
    },
    matchListItemText: {
        padding: '0px 0px 0px 15px'
    },
    listSimilarity: {
        padding : '10px'

    },
    matchOverall:{
        width: '100%',
        textAlign : 'center',
        '& p' : {
            color : '#09148f',
            padding : '0px',
            fontSize : '2.5rem',
            margin : '1rem'
        },
        '& span' : {
            backgroundColor : '#CCCCCC',
            padding : '10px'
            
        }
    }
  })

class DynamicBox extends Component{
    constructor(props) {    //improve pass table cell as table data through props
        super(props);
        this.state = {
            mdata : MATCHDATA,
        }
    }

    render(){
        const { classes } = this.props;
        return(
            <Container>
                <Typography variant="h2">Match Overview</Typography>  
                <List className={classes.matchlist}> 
                <Box className={classes.matchOverall}>
                    <p>21%</p>
                    <span>{this.state.mdata.length} matches</span> 
                </Box> 
                <Divider/>
                {this.state.mdata.map((row,index) => (
                    <ListItem divider className={classes.matchListItem}>
                        <Typography variant="h3" className={classes.listIndex}>
                            {++index}
                        </Typography>  
                        <ListItemText primary={row.string} secondary={row.sources} className={classes.matchListItemText}/> 
                        <Typography variant="h4" className={classes.listSimilarity}>
                            {row.similiarity}
                        </Typography>  
                    </ListItem>            
                ))}
                </List>
            </Container>         
        )
    }
}
export default withStyles(useStyles) (DynamicBox)

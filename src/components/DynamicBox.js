import React, { Component } from 'react';
import {MATCHDATA } from '../resources/MatchData';
import '../styles/media.scss';
import {Container,Typography} from '@material-ui/core';
import { List, ListItem, ListItemIcon, ListItemText } from '@material-ui/core';

const styles = {
    sideNav: {
        width: '100%',      
    },
    link: {
      color: 'black',
      textDecoration: 'none',
    }
  };

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
                <List>  
                {this.state.mdata.map((row,index) => (
                    <Box>
                        <Typography>
                        </Typography>
                        <ListItem>
                            <ListItemText primary={row.string} secondary={row.sources} />
                        </ListItem>
                    </Box>                        
                ))}
                </List>
            </Container>         
        )
    }
}
export default DynamicBox

import React, { Component, useState } from 'react';
import {AppBar,Drawer,Toolbar,Typography,Divider,IconButton,Box} from '@material-ui/core'
import MenuIcon from '@material-ui/icons/Menu';
import { List, ListItem, ListItemIcon, ListItemText } from '@material-ui/core';
import PermContactCalendarIcon from '@material-ui/icons/PermContactCalendar';
import AccountCircleIcon from '@material-ui/icons/AccountCircle';
import { Link } from 'react-router-dom';
import '../styles/media.scss';

const drawerWidth = 240;

const styles = {
    sideNav: {
        width: '15rem',      
    },
    link: {
      color: 'black',
      textDecoration: 'none',
    }
  };

export default class NavBar extends Component{
    constructor(props) {
        super(props)   
        this.state={
            isSideBarOpen: false
          }
    }

    toggleSideBar = () => {
        this.setState({
            isSideBarOpen: true,
        })
      }

    closeSideBar = () => {
        this.setState({
            isSideBarOpen: false,
        })
    }

    render(){
    const { isSideBarOpen } = this.state;
    return(
        <div>
            <AppBar position="static"> 
                <Toolbar>
                    <IconButton onClick={this.toggleSideBar}>
                        <MenuIcon/>
                    </IconButton>
                    <Typography variant="title" color="inherit">
                        {this.props.title}
                    </Typography>
                </Toolbar>
            </AppBar>
            <Drawer
                variant="temporary"
                open={isSideBarOpen}
                onClose={this.closeSideBar}>
                <Box style={styles.sideNav} >
                <List>
                    <Link to='/home' style={styles.link}>
                        <ListItem>
                        <ListItemIcon>
                            <AccountCircleIcon/>
                        </ListItemIcon>
                        <ListItemText primary='My Submission' />
                        </ListItem>
                    </Link>
                    <Divider/>
                    <Link to='/report' style={styles.link}>
                        <ListItem>
                        <ListItemIcon>
                            <PermContactCalendarIcon/>
                        </ListItemIcon>
                        <ListItemText primary='Report' />
                        </ListItem>
                    </Link>
                </List>
                </Box>
            </Drawer>   
        </div>
    )
    }
}

import React from 'react';
import {Button,makeStyles} from '@material-ui/core';

const useStyles = makeStyles(theme => ({
    buttonBlock : {
        margin : '0.2rem',
        borderRadius: '10px',
        fontWeight: '600',
        cursor: 'pointer',
        boxShadow: '0 4px 20px 0 rgba(61, 71, 82, 0.1), 0 0 0 0 rgba(0, 127, 255, 0)',
        '&:hover' : {
            backgroundColor:'#1a0387',
            transition: 'width 2s',
          }
      },
      input : {
          display : 'none'
      }
}))

function SignInButton(props){
    const classes = useStyles();
    const {title,type} = props;
    
    return(
        <Button
            color="primary"
            size="medium"
            variant="contained"
            fullWidth
            className={classes.buttonBlock}
            type={type}>
            {title}
        </Button>
    )
}

function MyButton(props){
    const classes = useStyles();
    const {title,type} = props;
    
    return(
        <Button
            color="primary"
            size="medium"
            variant="contained"
            component="span"
            className={classes.buttonBlock}
            type={type}>
            {title}
        </Button>
    )
}

function UploadButton(props){
    const {title,type} = props;
    return (
        <div style={{ display: 'inline' }}>
            <input
                type="file"
                accept="image/*"
                style={{ display: 'none' }}
                id="uploadButton"
            />
            <label htmlFor="uploadButton">
                <MyButton title={title} type={type} />
            </label>
        </div>
    )
}

export default function CustomButton(props){
    const {title,type} = props;

    if(type=='upload'){
        return <UploadButton title={title} type={type} />
    }else if(type=='submit'){
        return <SignInButton title={title} type={type} />
    }else{
        return <MyButton title={title} type={type} />
    }
}
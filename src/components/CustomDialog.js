import * as React from 'react';
import { Paper, Dialog,DialogContent,Button } from '@material-ui/core';
import Image from 'material-ui-image'
import PropTypes from 'prop-types';

export default function CustomDialog(props) {
    const  { open, onClose, data } = props;

  const handleClose = () => {
    onClose();
  };

  return (
    <Dialog onClose={handleClose} open={open}>
        <Paper>
            <DialogContent>My dialog content</DialogContent>
        </Paper>
        <Image src={data}/>
        <Button onClick={handleClose} color="primary">
                  CLOSE
        </Button>
    </Dialog>
  )
}

// CustomDialog.propTypes = {
//     onClose: PropTypes.func.isRequired,
//     open: PropTypes.bool.isRequired,
//   };
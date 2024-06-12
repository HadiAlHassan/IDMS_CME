import React, { useState, useEffect } from 'react';
import axios from 'axios';


function HelloWorld() {
    const [message, setMessage] = useState('');
  
    useEffect(() => {
      axios.get('http://127.0.0.1:8000/api/hello-world')
        .then(response => {
          setMessage(response.data.message);
        })
        .catch(error => {
          console.log(error);
        });
    }, []);
  
    return (
      <div>
        <h1>This message is sent from the frontend!</h1>
        <p>{message}</p>
      </div>
    );
  }
  
  export default HelloWorld;
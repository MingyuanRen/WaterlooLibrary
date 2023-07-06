import React from 'react';
import { useSelector } from 'react-redux';

export const Home = () => {
  const user = useSelector(state => state.user); 
  console.log("wdw", user)

  return (
    <div>
      <h1>Welcome {user ? user.name : ''}!</h1>
      {/* your other code... */}
    </div>
  );
};

import React, { useState } from "react";
import axios from "axios";

function App() {
  const [numbers, setNumbers] = useState([7, 2, 9, 3, 6]);
  const [sortedNumbers, setSortedNumbers] = useState([]);

  const sendArrayToFlask = async () => {
    try {
      const response = await axios.post("http://localhost:8000/api/sort", {
        numbers: numbers,
      });
      setSortedNumbers(response.data.sorted_numbers);
    } catch (error) {
      console.error("Error sending data to Flask:", error);
    }
  };

  return (
    <div>
      <h1>أنا بكلم بايثون يا رجااااالة شوفوا دي</h1>
      <h3>Original Array: {JSON.stringify(numbers)}</h3>
      <button onClick={sendArrayToFlask}>Sort Array</button>
      <h3>Sorted Array: {JSON.stringify(sortedNumbers)}</h3>
    </div>
  );
}

export default App;

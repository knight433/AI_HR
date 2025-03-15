// import { useEffect, useState } from "react";

// function Home() {
//   const [data, setData] = useState(null);

//   useEffect(() => {
//     fetch("http://127.0.0.1:5000/test")
//       .then(response => response.json())
//       .then(data => setData(data.testing))
//       .catch(error => console.error("Error fetching data:", error));
//   }, []);

//   return (
//     <div>
//       <h1>Flask Data:</h1>
//       {data ? <p>{JSON.stringify(data)}</p> : <p>Loading...</p>}
//     </div>
//   );
// }

// export default Home;

import React from "react";
import TreeBoxes from "./components/TreeBoxes";

function App() {
  return (
    <div>
      <h1>Tree-Based Dynamic Boxes</h1>
      <TreeBoxes />
    </div>
  );
}

export default App;

import './App.css';
import { Routes, Route } from 'react-router-dom';
import Navbar from './Navbar/Navbar';
import AddSong from './AddSong/AddSong';
import Songs from './Songs/Songs';
import Status from './Status/Status';


function App() {
  return (
    <div className="App">
      <Navbar />
      <Routes>
        <Route path='/' element={<AddSong />} />
        <Route path='results' element={<Songs />} />
        <Route path='status' element={<Status />} />
      </Routes>
    </div>
  );
}

export default App;

import InputLabel from "@mui/material/InputLabel";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";
import { useState } from "react";
import classes from "./Select.module.css";
const names = [
  "Oliver Hansen",
  "Van Henry",
  "April Tucker",
  "Ralph Hubbard",
  "Omar Alexander",
  "Carlos Abbott",
  "Miriam Wagner",
  "Bradley Wilkersonwegfdissssnnhiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiirgg",
  "Virginia Andrews",
  "Kelly Snyder",
];

function MultipleSelectNative(props) {
  const [personName, setPersonName] = useState([]);
  const handleChangeMultiple = (event) => {
    const { options } = event.target;
    const value = [];
    for (let i = 0, l = options.length; i < l; i += 1) {
      if (options[i].selected) {
        value.push(options[i].value);
      }
    }
    setPersonName(value);
  };
  const filteredNames = names.filter((name) =>
    name.toLowerCase().includes(props.searchInput.toLowerCase())
  );
  return (
    <div>
      <FormControl sx={{ py: 1, m: 2, minWidth: 120, maxWidth: 3000 }}>
        <InputLabel htmlFor="select-multiple-native">Pdfs</InputLabel>
        <Select
          multiple
          native
          value={personName}
          onChange={handleChangeMultiple}
          label="Native"
          inputProps={{
            id: "select-multiple-native",
          }}
        >
          {filteredNames.map((name) => (
            <option key={name} value={name}>
              {name}
            </option>
          ))}
        </Select>
      </FormControl>
    </div>
  );
}

export default MultipleSelectNative;

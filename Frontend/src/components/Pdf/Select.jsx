import InputLabel from "@mui/material/InputLabel";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";
import { useState, useEffect } from "react";
import classes from "./Select.module.css";

function MultipleSelectNative(props) {
  const [personName, setPersonName] = useState([]);
  const [names, setNames] = useState([]);

  useEffect(() => {
    const fetchPdfs = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/list-files/");
        const data = await response.json();
        if (Array.isArray(data.files)) {
          const pdfNames = data.files.map((pdf) => pdf.name);

          setNames(pdfNames);
        } else {
          console.error("Expected an array but got:", typeof data.files);
        }
      } catch (error) {
        console.error("Error fetching PDF names:", error);
      }
    };
    fetchPdfs();
  }, []);

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
      <FormControl
        className={classes.FormControl}
        sx={{
          py: 1,
          m: 2,
          minWidth: "90%",
          maxWidth: "90%",
        }}
      >
        <InputLabel shrink htmlFor="select-multiple-native">
          PDFs
        </InputLabel>
        <Select
          multiple
          native
          sx={{
            "&:hover .MuiOutlinedInput-notchedOutline": {
              borderColor: "#f2f2f2",
            },
            "&.Mui-focused .MuiOutlinedInput-notchedOutline": {
              borderColor: "#f2f2f2",
            },
          }}
          value={personName}
          onChange={handleChangeMultiple}
          label="Native"
          inputProps={{
            id: "select-multiple-native",
          }}
          className={classes.select}
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

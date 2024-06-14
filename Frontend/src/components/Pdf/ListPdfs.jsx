import * as React from 'react';
import Button from '@mui/material/Button';
import SearchIcon from '@mui/icons-material/Search';

function ListPdfs() {
    return (
        <div>
            <Button
                style={{
                    borderRadius: 10,
                    backgroundColor: "#1769aa",
                    padding: "10px",
                    fontSize: "13px",
                }}
                variant="contained"
                startIcon={<SearchIcon/>}
            >
                List PDFs
            </Button>
        </div>
    );
}
export default ListPdfs;
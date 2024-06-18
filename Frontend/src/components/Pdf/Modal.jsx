import Modal from "@mui/material/Modal";
import classes from "./Modal.module.css";
import IconButton from "@mui/material/IconButton";
import CloseIcon from "@mui/icons-material/Close";
import MultipleSelectNative from "./Select";
import styles from "./Select.module.css";
function BasicModal(props) {
  const handleClose = () => props.setOpen(false);

  return (
    <div className="Modal Container">
      <Modal
        open={props.open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <div className="Open Modal Container">
          <form className={classes.form}>
            <IconButton className={classes.actions} onClick={handleClose}>
              <CloseIcon />
            </IconButton>
            <p>
              <label htmlFor="search">Search for a PDF</label>
              <input
                type="text"
                id="pdfname"
                value={props.searchInput}
                onChange={(userSearch) =>
                  props.setSearchInput(userSearch.target.value)
                }
              />
            </p>
            <div className="Multiple Select Container">
              <MultipleSelectNative
                className={styles.formControl}
                searchInput={props.searchInput}
                id="select-multiple-native"
              />
            </div>
          </form>
        </div>
      </Modal>
    </div>
  );
}
export default BasicModal;

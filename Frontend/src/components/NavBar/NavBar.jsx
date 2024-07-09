import * as React from "react";
import Box from "@mui/material/Box";
import Drawer from "@mui/material/Drawer";
import { IconButton } from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import List from "@mui/material/List";
import Divider from "@mui/material/Divider";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import DashboardIcon from "@mui/icons-material/Dashboard";
import FolderIcon from "@mui/icons-material/Folder";
import PeopleIcon from "@mui/icons-material/People";
import EventIcon from "@mui/icons-material/Event";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";
import LogoutButton from "../LogOutButton/LogoutButton";
import classes from "./NavBar.module.css";
import { useNavigate } from "react-router-dom";

export default function NavBar() {
  const [open, setOpen] = React.useState(false);
  const navigate = useNavigate();

  const toggleDrawer = (newOpen) => () => {
    setOpen(newOpen);
  };

  const handleNavigation = (path) => {
    navigate(path);
    setOpen(false);
  };
  const DrawerList = (
    <Box sx={{ width: 250 }} role="presentation" onClick={toggleDrawer(false)}>
      <List>
        {[
          { text: "Profile", icon: <AccountCircleIcon />, path: "/profile" },
          { text: "Dashboard", icon: <DashboardIcon />, path: "/homepage" },
          { text: "Cases", icon: <FolderIcon />, path: "/cases" },
          { text: "Clients", icon: <PeopleIcon />, path: "/clients" },
          { text: "Calendar", icon: <EventIcon />, path: "/calendar" },
        ].map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton onClick={() => handleNavigation(item.path)}>
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
      <Divider />
      <LogoutButton />
    </Box>
  );

  return (
    <div>
      <IconButton
        className={classes.NavBarButton}
        variant="outlined"
        color="inherit"
        onClick={toggleDrawer(true)}
      >
        <MenuIcon />
      </IconButton>
      <Drawer open={open} onClose={toggleDrawer(false)}>
        {DrawerList}
      </Drawer>
    </div>
  );
}

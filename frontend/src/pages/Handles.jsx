import Heading from "../ui/Heading.jsx";
import Row from "../ui/Row.jsx";
import { FaDatabase } from "react-icons/fa6";
import FormFileUpdate from "../features/handles/FormFileUpdate.jsx";
import FormHandleUpdate from "../features/handles/FormHandleUpdate.jsx";

function Handles() {
  return (
    <>
      <Heading as="h1">
        <FaDatabase />
        Edit Handles
      </Heading>
      <Row type="filled">
        <FormFileUpdate />
        <FormHandleUpdate />
      </Row>
    </>
  );
}

export default Handles;

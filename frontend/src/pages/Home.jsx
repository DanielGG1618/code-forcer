import Row from "../ui/Row.jsx";
import Heading from "../ui/Heading.jsx";
import Card from "../ui/Card.jsx";
import { HiHome } from "react-icons/hi2";
import { SiCodeforces } from "react-icons/si";
import { FaDatabase } from "react-icons/fa6";
import { Description } from "../ui/Description.jsx";

function Home() {
  return (
    <>
      <Heading as="h1">
        <HiHome />
        Home page
      </Heading>
      <Description>
        <strong>
          Welcome to our website! Here you can easily manage CodeForces handlers
          and get the results of the contest you are interested in, easily find
          inconsistencies in handlers and distribute points for completing
          specific tasks. Enjoy easy navigation and efficient controls at your
          fingertips!
        </strong>
        {/*<span>
          For students, after logging into the university system, you can enter
          your CodeForces username so that the TA responsible for checking can
          put your grade.
        </span>*/}
      </Description>
      <Row type="filled">
        <Card
          title="Download Submissions"
          icon={SiCodeforces}
          to="/contests"
        />
        {/*<Card title="Submit Grades" icon={SiMoodle} to="/submit" />*/}
        <Card title="Edit Handles" icon={FaDatabase} to="/handles" />
      </Row>
    </>
  );
}

export default Home;

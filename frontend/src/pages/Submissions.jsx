import Heading from "../ui/Heading.jsx";
import { SiCodeforces } from "react-icons/si";
import { Description } from "../ui/Description.jsx";
import GetContestForm from "../features/codeforces/GetContestForm.jsx";

function Submissions() {
  return (
    <>
      <Heading as="h1">
        <SiCodeforces />
        Download Submissions
      </Heading>
      <Description>
        <p>You can copy the link by opening the context of interest</p>
        <p>
          To create or copy keys, go to{" "}
          <a href="https://codeforces.com/settings/api" target="_blank">
            your codeforces account settings page
          </a>
        </p>
      </Description>
      <GetContestForm />
    </>
  );
}

export default Submissions;

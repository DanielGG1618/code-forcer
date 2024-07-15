import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { BsFillArrowLeftSquareFill } from "react-icons/bs";
import { useForm } from "react-hook-form";
import { handlePostRequest } from "../../api/contests.js";
import { useLocalStorageState } from "../../hooks/useLocalStorage.js";
import { Link, useNavigate } from "react-router-dom";
import {
  StyledCover,
  ButtonBack,
  Description,
  List,
  Item,
  ItemRow,
  ItemInput,
  Error,
  UndefinedUsersList,
  UndefinedDescription,
  LateSubmissionsContainer,
  TimeConfiguration,
} from "./SubmissionsInfo.components.jsx";
import Button from "../../ui/Button.jsx";
import Heading from "../../ui/Heading.jsx";
import SpinnerMini from "../../ui/SpinnnerMini.jsx";
import FormElement from "../../ui/FormElement.jsx";
import Input from "../../ui/Input.jsx";

function SubmissionsInfo({ info }) {
  const definedUsers = {
    ...info,
    problems: info.problems.map((item) => {
      return {
        ...item,
        submissions: item.submissions.filter(
          (item) => item.author.email != null,
        ),
      };
    }),
  };
  const unpossibleReqest = definedUsers.problems.every(
    (item) => item.submissions.length === 0,
  );

  const navigate = useNavigate();

  const [contestInfo, setContestInfo] = useLocalStorageState(
    {},
    `contest-${info.id}`,
  );

  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
  } = useForm();

  useEffect(() => {
    const subscription = watch((value) => {
      for (let key in value) {
        value[key] = parseFloat(value[key]);
      }
      setContestInfo(value);
    });
    return () => subscription.unsubscribe();
  }, [setContestInfo, watch]);

  const [isGetting, setIsGetting] = useState(false);

  let filename;

  const onSubmit = function (data) {
    setIsGetting(true);

    handlePostRequest(definedUsers, data)
      .then((res) => {
        filename = res.headers
          .get("content-disposition")
          .match(/(?<=")(?:\\.|[^"\\])*(?=")/)[0];
        return res.blob();
      })
      .then((blob) => {
        const url = window.URL.createObjectURL(new Blob([blob]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", filename || "grades");

        // Append to html link element page
        document.body.appendChild(link);

        // Start download
        link.click();

        // Clean up and remove the link
        link.parentNode.removeChild(link);
      })
      .catch((err) => {
        toast.error(err.message);
      })
      .finally(() => {
        setIsGetting(false);
      });
  };

  return (
    <StyledCover>
      <ButtonBack onClick={() => navigate("/submissions")}>
        <BsFillArrowLeftSquareFill />
      </ButtonBack>
      <Heading as="h2">Contest &quot;{info.name}&quot;</Heading>
      <Description>
        Total number of problems: {info.problems.length}
      </Description>
      <List onSubmit={handleSubmit(onSubmit)}>
        {info.problems.map((item, index) => (
          <SubmissionItem key={index} item={item} index={index}>
            <>
              <strong>
                {item.index} (&quot;{item.name}&quot;)
              </strong>
              <ItemInput
                placeholder="Maximum points per task"
                data-index={index}
                disabled={isGetting}
                defaultValue={contestInfo[index.toString()] || null}
                {...register(`${index}`, {
                  required: "This field is required",
                  pattern: {
                    value: /^\d*\.?\d*$/,
                    message: "Incorrect value",
                  },
                })}
              />
              {errors[`${index}`] && (
                <Error>{errors[`${index}`].message}</Error>
              )}
            </>
          </SubmissionItem>
        ))}
        <SubmissionsSettings
          isGetting={isGetting}
          register={register}
          contestInfo={contestInfo}
        />
        {unpossibleReqest ? (
          <UndefinedDescription style={{ fontWeight: "400" }}>
            There are no solutions that could be obtained, please{" "}
            <b>wait for the end of the contest</b> or{" "}
            <Link to="/handles">download the handles</Link> of the participants
          </UndefinedDescription>
        ) : (
          <Button disabled={isGetting} type="submit">
            {isGetting ? <SpinnerMini /> : "Create a rating file"}
          </Button>
        )}
      </List>
    </StyledCover>
  );
}

function SubmissionsSettings({ register, isGetting, contestInfo }) {
  return (
    <LateSubmissionsContainer>
      <Heading as="h2">Late Submission Configuration</Heading>
      <Heading as="h3" style={{ gridColumn: "span 3" }}>
        Additional time for late submission
      </Heading>
      <TimeConfiguration>
        <FormElement label="Days" borderless={true}>
          <Input
            disabled={isGetting}
            placeholder={0}
            defaultValue={contestInfo["additional-days"] || null}
            {...register("additional-days", {
              min: 0,
            })}
            style={{ textAlign: "center" }}
          />
        </FormElement>
        <FormElement label="Hours" borderless={true}>
          <Input
            disabled={isGetting}
            placeholder={0}
            defaultValue={contestInfo["additional-hours"] || null}
            {...register("additional-hours", {
              min: 0,
            })}
            style={{ textAlign: "center" }}
          />
        </FormElement>
        <FormElement label="Minutes" borderless={true}>
          <Input
            disabled={isGetting}
            placeholder={0}
            defaultValue={contestInfo["additional-minutes"] || null}
            {...register("additional-minutes", {
              min: 0,
            })}
            style={{ textAlign: "center" }}
          />
        </FormElement>
      </TimeConfiguration>
      <FormElement label="Penalty percentage" borderless={true}>
        <Input
          disabled={isGetting}
          placeholder={20}
          defaultValue={contestInfo["penalty"] || null}
          {...register("penalty", { min: 0 })}
          style={{ textAlign: "center" }}
        />
      </FormElement>
    </LateSubmissionsContainer>
  );
}

function SubmissionItem({ index, item, children }) {
  const undefinedUsers = item.submissions.filter((item) => !item.author.email);
  const [isOpen, setIsOpen] = useState(false);

  return (
    <Item undefined={undefinedUsers.length}>
      {children}
      <ItemRow>
        <span>
          Total number of sumbissions:
          <strong>{item?.submissions?.length}</strong>
        </span>

        {undefinedUsers.length > 0 ? (
          <span>
            Undefined participants: <strong>{undefinedUsers?.length}</strong>
            <Button
              size="small"
              type="button"
              onClick={() => setIsOpen((open) => !open)}
            >
              {!isOpen ? "SHOW" : "HIDE"}
            </Button>
          </span>
        ) : (
          <span>All users are defined</span>
        )}
      </ItemRow>
      {isOpen && (
        <UndefinedUsersList id={`list-${index}`}>
          {undefinedUsers.map((user) => (
            <span key={user?.author?.handle}>{user?.author?.handle}</span>
          ))}
        </UndefinedUsersList>
      )}
    </Item>
  );
}

export default SubmissionsInfo;

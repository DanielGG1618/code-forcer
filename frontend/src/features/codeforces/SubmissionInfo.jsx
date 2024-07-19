import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { BsFillArrowLeftSquareFill } from "react-icons/bs";
import { useForm, Controller } from "react-hook-form";
import { handlePostRequest } from "../../api/contests.js";
import { useLocalStorageState } from "../../hooks/useLocalStorage.js";
import { Link, useNavigate } from "react-router-dom";
import Select from "react-select";

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
  SubmissionsAction,
} from "./SubmissionsInfo.components.jsx";
import Button from "../../ui/Button.jsx";
import Heading from "../../ui/Heading.jsx";
import SpinnerMini from "../../ui/SpinnnerMini.jsx";
import FormElement from "../../ui/FormElement.jsx";
import Input from "../../ui/Input.jsx";

const selectStyles = {
  container: (baseStyles) => ({
    ...baseStyles,
    fontSize: "1.4rem",
    height: "4.5rem",
  }),
  control: (baseStyles) => ({
    ...baseStyles,
    height: "4.5rem",
  }),
};
const selectTheme = (theme) => ({
  ...theme,
  colors: {
    ...theme.colors,
    primary: "var(--color-brand-600)",
    primary75: "var(--color-brand-500)",
    primary50: "var(--color-brand-400)",
    primary25: "var(--color-brand-400)",
    danger: "var(--color-red-700)",
    dangerLight: "var(--color-red-100)",
    neutral0: "var(--color-grey-0)",
    neutral5: "var(--color-grey-50)",
    neutral10: "var(--color-grey-100)",
    neutral20: "var(--color-grey-200)",
    neutral30: "var(--color-grey-300)",
    neutral40: "var(--color-grey-400)",
    neutral50: "var(--color-grey-500)",
    neutral60: "var(--color-grey-600)",
    neutral70: "var(--color-grey-700)",
    neutral80: "var(--color-grey-800)",
    neutral90: "var(--color-grey-900)",
  },
});

function SubmissionsInfo({ info, selectors }) {
  const options = selectors?.map((el) => {
    return {
      value: el,
      label: el.slice(0, 1).toUpperCase() + el.slice(1),
    };
  });
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
    control,
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
    data = data.selector ? data : { ...data, selector: options[0] };

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
      <ButtonBack onClick={() => navigate("/contests")}>
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
          <SubmissionsAction>
            <Controller
              control={control}
              name="selector"
              render={({ field }) => (
                <Select
                  {...field}
                  placeholder="Choose submission type"
                  theme={selectTheme}
                  styles={selectStyles}
                  options={options}
                />
              )}
            />
            <Button disabled={isGetting} type="submit">
              {isGetting ? <SpinnerMini /> : "Create a rating file"}
            </Button>
          </SubmissionsAction>
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
          {...register("penalty", {
            min: {
              value: 0,
              message: "Can not be negative",
            },
            max: {
              value: 100,
              message: "Maxium penalty is 100%",
            },
          })}
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

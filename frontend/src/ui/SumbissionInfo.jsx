import styled from "styled-components";
import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import Heading from "./Heading.jsx";
import Input from "./Input.jsx";
import { BsFillArrowLeftSquareFill } from "react-icons/bs";
import { useForm } from "react-hook-form";
import Button from "./Button.jsx";
import SpinnerMini from "./SpinnnerMini.jsx";
import { useMoveBack } from "../hooks/useMoveBack.js";
import { handlePostRequest } from "../api/contests.js";
import { useLocalStorageState } from "../hooks/useLocalStorage.js";
import { Link } from "react-router-dom";

const StyledCover = styled.div`
  position: relative;
  max-width: 90rem;
  gap: 1rem;

  text-align: center;
  color: var(--color-grey-600);
  font-size: 1.6rem;
  font-weight: 500;
  padding: 3rem 4.5rem 5rem;
  transition: all 0.3s;
  box-shadow: var(--shadow-md);
  border-radius: var(--border-radius-md);
`;

const ButtonBack = styled.button`
  position: absolute;
  left: 2rem;
  top: 2rem;
  background-color: transparent;
  border: none;

  svg {
    width: 5rem;
    height: 5rem;
    transition: fill 0.3s ease;
  }
  &:hover svg {
    fill: var(--color-brand-600);
  }
`;

const Description = styled.div`
  display: flex;
  justify-content: center;

  &:not(:last-child) {
    margin-bottom: 3.5rem;
  }
`;

const List = styled.form`
  margin: 0 auto;
  max-width: 60rem;
`;
const Item = styled.div`
  position: relative;
  display: flex;
  flex-direction: column;
  padding-bottom: 2rem;
  column-gap: 0.8rem;

  font-weight: 400;

  &:not(:last-child) {
    margin-bottom: 2rem;
    border-bottom: 1px solid var(--color-grey-200);
  }

  strong {
    font-weight: 500;
  }

  > strong {
    font-size: 2rem;
  }
  > strong:not(:last-child) {
    margin-bottom: 1.5rem;
  }
  > input:not(:last-child) {
    margin-bottom: 0.2rem;
  }
`;

const ItemRow = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2.5rem;
  margin-top: 2rem;

  span {
    display: inline-flex;
    align-items: center;
    gap: 1rem;
  }
  span strong {
    align-self: flex-start;
    font-size: 2rem;
    padding-bottom: 0.3rem;
  }
`;

const ItemInput = styled(Input)`
  max-width: 20rem;
  margin: 0 auto;
  text-align: center;
  padding: 0.3rem 1rem;
  font-size: 1.4rem;

  &:not(:last-child) {
    margin-bottom: 0.5rem;
  }
`;

const Error = styled.span`
  font-size: 1.4rem;
  color: var(--color-red-700);
`;

const UndefinedUsersList = styled.div`
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  row-gap: 0.6rem;
  column-gap: 1.2rem;
  margin-top: 2rem;

  & span {
    position: relative;
    display: inline-flex;
    align-items: center;
    gap: 0.6rem;
  }
  & span::before {
    content: "";
    flex: 0 0 0.3rem;
    width: 0.3rem;
    height: 0.3rem;
    border-radius: 100%;
    background-color: var(--color-grey-700);
  }
`;

const UndefinedDescription = styled.p`
  padding: 2rem 2.5rem;
  border: 2px solid var(--color-red-400);
  border-radius: var(--border-radius-md);

  font-weight: 400;
  b {
    font-weight: 500;
  }
  a {
    font-weight: 500;
    text-decoration: underline;
  }
`;

function SumbissionsInfo({ info }) {
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
  console.log(unpossibleReqest);

  const moveBack = useMoveBack();
  const [contestPoints, setContestPoints] = useLocalStorageState(
    [],
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
      setContestPoints(
        Object.values(value).map((item) => parseFloat(item) || undefined),
      );
    });
    return () => subscription.unsubscribe();
  }, [setContestPoints, watch]);

  const [isGetting, setIsGetting] = useState(false);

  const onSubmit = function (data) {
    setIsGetting(true);

    handlePostRequest(definedUsers, data)
      .then((res) => {
        return res.blob();
      })
      .then((blob) => {
        var file = window.URL.createObjectURL(blob);
        window.location.assign(file);
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
      <ButtonBack onClick={moveBack}>
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
                defaultValue={contestPoints[index]}
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

function SubmissionItem({ index, item, children }) {
  const undefinedUsers = item.submissions.filter((item) => !item.author.email);
  const [isOpen, setIsOpen] = useState(false);

  return (
    <Item>
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
export default SumbissionsInfo;

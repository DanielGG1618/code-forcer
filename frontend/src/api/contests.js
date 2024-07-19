export async function getContest(contestID, APIKey, secretKey) {
  const url = `/contests/${contestID}?key=${APIKey}&secret=${secretKey}`;

  const response = await fetch(url);

  if (!response.ok) {
    throw response;
  }

  const data = await response.json();
  return data;
}
export async function getSelectors() {
  const url = `/submission-selectors`;
  const response = await fetch(url);

  if (!response.ok) {
    throw response;
  }

  const data = await response.json();
  return data;
}
export async function handlePostRequest(info, data) {
  const penalty = data.penalty ? parseFloat(data.penalty) / 100 : 0;
  const additionTime =
    parseFloat(data["additional-days"] ? data["additional-days"] : 0) * 86400 +
    parseFloat(data["additional-hours"] ? data["additional-hours"] : 0) * 3600 +
    parseFloat(data["additional-minutes"] ? data["additional-minutes"] : 0) *
      60;
  const url = `/moodle_grades`;

  const body = {
    contest: {
      ...info,
      problems: info.problems.map((item, index) => {
        return {
          ...item,
          max_grade: parseFloat(data[`${index}`]),
          submissions: item.submissions.map((item) => {
            return {
              ...item,
              author_email: item.author.email,
            };
          }),
        };
      }),
    },
    legal_excuses: {},
    late_submission_policy: {
      penalty: penalty < 0 ? 0 : penalty > 1 ? 1 : penalty,
      extra_time: additionTime,
    },
    submission_selector_name: data.selector.value,
  };

  console.log("Body of request:", body);

  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json;charset=utf-8",
    },
    body: JSON.stringify(body),
  });

  console.log("Server answer for file generating", response);

  if (!response.ok) {
    throw new Error(response.statusText);
  }
  return response;
}

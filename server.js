const express = require("express");
const app = express();
const bodyParser = require('body-parser'); 
app.use(bodyParser.json());

const KPSDK_SOLVER = require('./src/index.js');

async function solve(pjs, path) {
    const {
        close,
        fetch,
        KPSDK_message
        
  } = await KPSDK_SOLVER({
      kasada: {
      configuration: [{
          domain: 'kick.com',
          method: 'POST',
          path: path,
        }
    ],
    sdk_script_url: pjs,
},
parent_url: 'https://kick.com'
});

console.log(KPSDK_message);

  const {
    route,
    request
  } = await fetch(`https://kick.com${path}`, {
    method: 'POST'
  });
  let res = request.headers();
  await route.continue();
  await close();
  return {
      "user-agent": res["user-agent"],
      "x-kpsdk-ct": res["x-kpsdk-ct"],
      "x-kpsdk-cd": res["x-kpsdk-cd"]
    }
}

app.post("/solve", (req, res) => {
    solve(req.body.pjs, req.body.path).then((response) => {
        res.json(response)
    })
})



app.listen(3033, () => {
    console.log("Server started")
})
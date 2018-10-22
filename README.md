# CloudServicesInterface
Simple interface for demo

## Dependencies

* Please make sure following dependencies are installed:
  ```
  python==2.7.12
  Flask==0.12.2
  boto3==1.9.27
  request==2.18.4
  ```
## FAQ

Q1. Why do you adding additional field `lst_instance_states` in restful request for filtering different instances states?
* Ans: The spec I'm having here states 設計一個 API 可以  query 目前一個固定用戶的各種雲帳號底下有多少台已經**開啟**的虛擬服務機, but I'm not sure **開啟** refers to **running** state or **the existence of instances**. As a result, for preventing any misunderstanding here, if user can specify their filtering requirement, it would be easier. Nevertheless, it's totally **OKAY** if user just leave it as an empty list, CloudInterface would return the number of all instances which existed **(not terminated)** under the user account.

Q2. Why do you adding additional field `user` in restful request for filtering different instances states?
* Ans: For making sure user can use specific profile to query the corresponding information

Q3. What's the availble options in lst_instance_states field?
* Ans: I'm only implementing this interface based on AWS only, and thus available options would be the options which AWS supported in boto3 API, which including **(pending | running | shutting-down | terminated | stopping | stopped )**

Q4. What's the avalable region options in region field?
* Ans: As I mentioned above, this demo is focusing on AWS only for now, thus available options would the options which AWS supported in boto3 API, which listed at [AWS document](https://docs.aws.amazon.com/en_us/AmazonRDS/latest/UserGuide/Concepts.RegionsAndAvailabilityZones.html)

Q5. Why your design it with **HTTP POST action** instead of **GET**?
* Ans: From my point of view, if frontend can feed the data with a json array, it's going to be much more flexible for a single interface since all cloud vendor's information is aggregated into a json object. I can also make multiple **HTTP GET** actions and each of them handle one cloud vendor's information, but the requirements I have here is asking me to create **一個Restful/Graph Interface** to accomplish the tasks and thus I made it a HTTP POST here. 

## Usage  
0. Please provide the default value in **AWS_default.yaml**, below is a basic example
```
DefaultRegion: "us-east-1"
DefaultStates: "running,stopped,pending,shutting-down,terminated,stopping"
```

* Note that all fields in this file is a **MUST HAVE** information for cloud connector to query cloud service at default mode.
* Note that you should add another file for preparing default value while adding other cloud connector class. I'm not encourage user to set default value inside flask restful controller.

1. Please provide valid user credentials in credential.yaml, below is a basic example.
```
AWS: //Fixed field, indicating credential below is using for AWS cloud service connection.
  default: //user profile name, you can specify your own name, default is a MUST since it'll be used when there's no user profile preference in restful request.
    AccessKeyID: "Your AccessKeyID"
    SecretAccessKey: "Your SecretAccessKey"
```

* Note that **credential.yaml** should be at the same directory as **CloudInterface.py** is located.
* Note that **default** user profile is a **MUST HAVE** field for default scenario.

2. Starting flask server, flask server should be ready for accepting restful request from **`http://<your IP>:8080`**
  
```
root@flask-demo:~/aws_test# python CloudInterface.py
 * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 215-062-453
```

3. Open browser, enter **`http://<your IP>:8080`**, you should see a basic responding with `Hello World!`

4. For query all cloud vendor's VM, please send a **HTTP POST** request with json content below.
   ```
   {"lstQueryCloudVendors":[]}
   ```  
   Server reply should be like:
   ```
   {"Azure": "123", "AWS": "2"}
   ```

5. For query all existing instances with specific cloud vendor's information, please refer to the json content below.
   ```
   {
      "lstQueryCloudVendors":[
        {
          "vendor":"AWS",
          "user":"default",
          "region":"",
          "lst_instance_states":[]
        },
        {
          "vendor":"Azure",
          "user":"default",
          "region":"",
          "lst_instance_states":[]
        }
      ]
   }
   ```

6. For query all existing instances with running status among specific cloud vendor's information, please refer to the json content below.

  ```
  {
      "lstQueryCloudVendors":[
        {
          "vendor":"AWS",
          "user":"default",
          "region":"",
          "lst_instance_states":["running"]
        },
        {
          "vendor":"Azure",
          "user":"default",
          "region":"",
          "lst_instance_states":["running"]
        }
      ]
   }
  ```

  * Note that if user didn't specify any user account information in **user** field, CloudInterface would use `default` profile credential in `credential.yaml` to access cloud service.
  * Note that if user didn't specify any regional information in **region** field, CloudInterface would use regional information in **AWS_default.yaml** as default.

## Contact author

* **Chien-Ting(Jaxon) Chen** - *Initial work* - [CloudInteface](https://github.com/chientingchen/CloudServicesInterface)
* Please contact me whenever you have any question/issue with setting it up.

 


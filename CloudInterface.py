import boto3, json, os, yaml
from flask import Flask, request
from config import DevConfig

class BaseCloudConnector(object):
    cloud_vendor_name = None
    user_profile_name = None
    _CREDENTIAL_FILE_PATH = './'
    _CREDENTIAL_FILE_NAME = 'credential.yaml'

    def __init__(self, user_profile_name, lst_instance_states):
        self.lst_instance_states = lst_instance_states
        self.user_profile_name = user_profile_name

    def _get_credentials(self):
        raise NotImplementedError()
       
    def get_num_instances_based_on_states(self):
        raise NotImplementedError()

    @classmethod
    def CloudConnectorBasedOnName(cls, user_define_cloud_vendor_name):
        return cls.cloud_vendor_name == user_define_cloud_vendor_name

class AWSCloudConnector(BaseCloudConnector):
    
    cloud_vendor_name = 'AWS'

    def _get_credentials(self):
        
        dict_credentials = {}

        f = open(os.path.join(self._CREDENTIAL_FILE_PATH, self._CREDENTIAL_FILE_NAME))
        data = f.read()
        INPUT_DATA = yaml.load(data)
        f.close()
        
        dict_credentials.update({'AccessKeyID': INPUT_DATA['AWS'][self.user_profile_name]['AccessKeyID']})
        dict_credentials.update({'SecretAccessKey': INPUT_DATA['AWS'][self.user_profile_name]['SecretAccessKey']})
        
        return dict_credentials

    def get_num_instances_based_on_states(self):
        session = boto3.Session(
                  aws_access_key_id = self._get_credentials()['AccessKeyID'],
                  aws_secret_access_key= self._get_credentials()['SecretAccessKey'],
                 )
        client = session.client('ec2')

        dict_filters = {'Name': 'instance-state-name','Values': []}
        for value in self.lst_instance_states:
            dict_filters['Values'].append(value)

        lst_filters = [dict_filters]

        if len(self.lst_instance_states) > 0:
            json_aws_ret = client.describe_instances(Filters=lst_filters)
        else:
            json_aws_ret = client.describe_instances()

        return len(json_aws_ret['Reservations'])

class AzureCloudConnector(BaseCloudConnector): #Create another cloud connector based on base class.
    cloud_vendor_name = 'Azure'

    def get_credentials(self):
        return {}

    def get_num_instances_based_on_states(self):
        return 123

class FactoryCloudConnector(object):
    lst_CloudConnectors = [AWSCloudConnector, AzureCloudConnector] #Adding extra cloud connector class here.

    def __init__(self, cloud_vendor_name, user_profile_name, lst_instance_states=[]):
        self.lst_instance_states = lst_instance_states
        self.cloud_vendor_name = cloud_vendor_name
        self.user_profile_name = user_profile_name
        self.cloudconnector = self.choose_cloud_connector()

    def choose_cloud_connector(self):
        for CloudConnector in self.lst_CloudConnectors:
            if CloudConnector.CloudConnectorBasedOnName(self.cloud_vendor_name): 
                return CloudConnector(self.user_profile_name, self.lst_instance_states)

    def get_num_instances_based_on_states(self):
        return self.cloudconnector.get_num_instances_based_on_states()

app = Flask(__name__)
app.config.from_object(DevConfig)

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/',methods=['POST'])
def index_post():
    print 'data:'
    print '----------------------------data---------------------------------'
    print request.get_json()
    data = request.get_json()
    print '----------------------------end of data--------------------------'

    ret_dict = {}

    if len(data['lstQueryCloudVendors']) == 0: #Adding new default vendor informtaion here.
        data['lstQueryCloudVendors'].append({"vendor":"AWS","user":"default","lst_instance_states":[]})
        data['lstQueryCloudVendors'].append({"vendor":"Azure","user":"default", "lst_instance_states":[]})

    
 
    for cloudvendor in data['lstQueryCloudVendors']:
        cloudconnector = FactoryCloudConnector(cloudvendor['vendor'], cloudvendor['user'] if len(cloudvendor['user']) > 0 else 'default', cloudvendor['lst_instance_states'])
        ret_dict.update({ cloudvendor['vendor']: str(cloudconnector.get_num_instances_based_on_states()) })

    return json.dumps(ret_dict)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)


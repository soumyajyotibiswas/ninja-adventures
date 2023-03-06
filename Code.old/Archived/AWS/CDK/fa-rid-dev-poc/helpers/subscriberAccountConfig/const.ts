export const appName = 'fa-rid'

export enum stageName {
    GAMMA = 'gamma',
    PROD = 'prod',
    POC = 'poc'
}

type awsAccountMap = {
    [key:string]:{[key:string]:string|string[]}
}

export const awsAccountMap : awsAccountMap = {
    'prod' : {
        'awsAccountId':'589629135297',
        'awsRegions': ['us-west-2']
    },
    'gamma' : {
        'awsAccountId':'883564835703',
        'awsRegions': ['us-east-1']
    },
    'poc' : {
        'awsAccountId':'883564835703',
        'awsRegions': ['ap-south-1']
    }
}
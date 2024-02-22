import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix, precision_score, recall_score, accuracy_score
import joblib
import argparse
import re
import seaborn as sn
import matplotlib.pyplot as plt
import logging

from azureml.core.run import Run
from azureml.core import Datastore, Dataset


class SpamClassification():
    def __init__(self, args):
        '''
        Initialize Steps
        ----------------
            1. Initalize Azure ML Run Object
            2. Create directories
        '''
        self.args = args
        self.run = Run.get_context()
        self.workspace = self.run.experiment.workspace
        os.makedirs('./model_metas', exist_ok=True)

    def get_files_from_datastore(self, container_name, file_name):
        '''
        Get the input CSV file from workspace's default data store
        Args :
            container_name : name of the container to look for input CSV
            file_name : input CSV file name inside the container
        Returns :
            data_ds : Azure ML Dataset object
        '''
        datastore_paths = [(self.datastore, os.path.join(container_name,file_name))]
        #data_ds = Dataset.Tabular.from_delimited_files(path=datastore_paths)
        data_ds = Dataset.File.from_files(path=datastore_paths)
        dataset_name = self.args.dataset_name     
        if dataset_name not in self.workspace.datasets:
            data_ds = data_ds.register(workspace=self.workspace,
                        name=dataset_name,
                        description=self.args.dataset_desc,
                        tags={'format': 'CSV'},
                        create_new_version=True)
        else:
            print('Dataset {} already in workspace '.format(dataset_name))
        return data_ds      

    def create_pipeline(self):
        '''
        SPAM Data training and Validation
        '''        
        self.datastore = Datastore.get(self.workspace, self.workspace.get_default_datastore().name)
        print("Received datastore")
        input_ds = self.get_files_from_datastore(self.args.container_name,self.args.input_csv)
        #final_df = input_ds.to_pandas_dataframe(encoding="latin-1")
        final_df = pd.read_csv(input_ds, encoding="latin-1")
        print("Input DF Info",final_df.info())
        print("Input DF Head",final_df.head())

        final_df['label'] = final_df['class'].map({'ham': 0, 'spam': 1})
        X = final_df['message']
        y = final_df['label']

        cv = CountVectorizer()
        X = cv.fit_transform(X)

        X_train,X_test,y_train,y_test=train_test_split(X, y, test_size=0.33, random_state=42)
        
        model = MultinomialNB()
        model.fit(X_train,y_train)
        y_pred = model.predict(X_test)
        print("Model Score : ", model.score(X_test,y_test))
        os.mkdir('models')
        joblib.dump(cv, self.args.cv_model_path)
        joblib.dump(model, self.args.model_path)

        self.validate(y_test, y_pred, X_test)

        match = re.search('([^\/]*)$', self.args.model_path)
        # Upload Model to Run artifacts
        self.run.upload_file(name=self.args.artifact_loc + match.group(1),
                                path_or_stream=self.args.model_path)

        print("Run Files : ", self.run.get_file_names())
        self.run.complete()

    def create_confusion_matrix(self, y_true, y_pred, name):
        '''
        Create confusion matrix
        '''
        try:
            confm = confusion_matrix(y_true, y_pred, labels=np.unique(y_pred))
            print("Shape : ", confm.shape)

            df_cm = pd.DataFrame(confm, columns=np.unique(y_true), index=np.unique(y_true))
            df_cm.index.name = 'Actual'
            df_cm.columns.name = 'Predicted'
            df_cm.to_csv(name+".csv", index=False)
            self.run.upload_file(name="./outputs/"+name+".csv",path_or_stream=name+".csv")

            plt.figure(figsize = (120,120))
            sn.set(font_scale=1.4)
            c_plot = sn.heatmap(df_cm, fmt="d", linewidths=.2, linecolor='black',cmap="Oranges", annot=True,annot_kws={"size": 16})
            plt.savefig("./outputs/"+name+".png")
            self.run.log_image(name=name, plot=plt)
        except Exception as e: 
            logging.error("Create consufion matrix Exception")

    def create_outputs(self, y_true, y_pred, X_test, name):
        '''
        Create prediction results as a CSV
        '''
        pred_output = {"Actual Species" : y_true['label'].values, "Predicted Species": y_pred['label'].values}        
        pred_df = pd.DataFrame(pred_output)
        pred_df = pred_df.reset_index()
        X_test = X_test.reset_index()
        final_df = pd.concat([X_test, pred_df], axis=1)
        final_df.to_csv(name+".csv", index=False)
        self.run.upload_file(name="./outputs/"+name+".csv",path_or_stream=name+".csv")

    def validate(self, y_true, y_pred, X_test):
        self.run.log(name="Precision", value=round(precision_score(y_true, y_pred, average='weighted'), 2))
        self.run.log(name="Recall", value=round(recall_score(y_true, y_pred, average='weighted'), 2))
        self.run.log(name="Accuracy", value=round(accuracy_score(y_true, y_pred), 2))

        self.create_confusion_matrix(y_true, y_pred, "confusion_matrix")

        y_pred_df = pd.DataFrame(y_pred, columns = ['label'])
        self.create_outputs(y_true, y_pred_df, X_test, "predictions")
        self.run.tag("SpamClassifierFinalRun")   

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='QA Code Indexing pipeline')
    parser.add_argument('--container_name', type=str, help='Path to default datastore container')
    parser.add_argument('--input_csv', type=str, help='Input CSV file')
    parser.add_argument('--dataset_name', type=str, help='Dataset name to store in workspace')
    parser.add_argument('--dataset_desc', type=str, help='Dataset description')
    parser.add_argument('--model_path', type=str, help='Path to store the model')
    parser.add_argument('--cv_model_path', type=str, help='Path to store the countvectorizer model')
    parser.add_argument('--artifact_loc', type=str, 
                        help='DevOps artifact location to store the model', default='')
    args = parser.parse_args()
    spam_classifier = SpamClassification(args)
    spam_classifier.create_pipeline()

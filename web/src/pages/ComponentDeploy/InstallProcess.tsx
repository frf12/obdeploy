import InstallProcessComp from '@/component/InstallProcessComp';
import {
  componentChangeLog,
  componentChangeTask,
} from '@/services/component-change/componentChange';
import { getErrorInfo } from '@/utils';
import { useModel } from '@umijs/max';
import { useRequest } from 'ahooks';
import NP from 'number-precision';
import { useEffect, useState } from 'react';

let timerProgress: NodeJS.Timer;
export default function InstallProcess() {
  const { setErrorVisible, setErrorsList, errorsList } = useModel('global');
  const {
    componentConfig,
    installStatus,
    setInstallStatus,
    setInstallFinished,
  } = useModel('componentDeploy');
  const name = componentConfig?.appname;
  const [progress, setProgress] = useState(0);
  const [showProgress, setShowProgress] = useState(0);
  const [currentPage, setCurrentPage] = useState(true);
  const [statusData, setStatusData] = useState<API.TaskInfo>({});
  const [logData, setLogData] = useState<API.InstallLog>({});

  const { run: fetchInstallStatus } = useRequest(componentChangeTask, {
    manual: true,
    onSuccess: ({ success, data }) => {
      if (success) {
        setStatusData(data || {});
        clearInterval(timerProgress);
        if (data?.status !== 'RUNNING') {
          setInstallStatus(data?.status);
          setCurrentPage(false);
          setTimeout(() => {
            setInstallFinished(true);
            setErrorVisible(false);
            setErrorsList([]);
          }, 2000);
        } else {
          setTimeout(() => {
            fetchInstallStatus({ name });
          }, 1000);
        }
        const newProgress = NP.divide(data?.finished, data?.total).toFixed(2);
        setProgress(newProgress);
        let step = NP.minus(newProgress, progress);
        let stepNum = 1;
        timerProgress = setInterval(() => {
          const currentProgressNumber = NP.plus(
            progress,
            NP.times(NP.divide(step, 100), stepNum),
          );

          if (currentProgressNumber >= 1) {
            clearInterval(timerProgress);
          } else {
            stepNum += 1;
            setShowProgress(currentProgressNumber);
          }
        }, 10);
      }
    },
    onError: (e) => {
      if (currentPage) {
        setTimeout(() => {
          fetchInstallStatus({ name });
        }, 1000);
      }
      const errorInfo = getErrorInfo(e);
      setErrorVisible(true);
      setErrorsList([...errorsList, errorInfo]);
    },
  });

  const { run: handleInstallLog } = useRequest(componentChangeLog, {
    manual: true,
    onSuccess: ({ success, data }) => {
      if (success && installStatus === 'RUNNING') {
        setLogData(data || {});
        setTimeout(() => {
          handleInstallLog({ name });
        }, 1000);
      }
    },
    onError: (e) => {
      if (installStatus === 'RUNNING' && currentPage) {
        setTimeout(() => {
          handleInstallLog({ name });
        }, 1000);
      }
      const errorInfo = getErrorInfo(e);
      setErrorVisible(true);
      setErrorsList([...errorsList, errorInfo]);
    },
  });

  useEffect(() => {
    if (name) {
      fetchInstallStatus({ name });
      handleInstallLog({ name });
    }
  }, [name]);

  return (
    <InstallProcessComp
      logData={logData}
      installStatus={installStatus}
      statusData={statusData}
      showProgress={showProgress}
    />
  );
}
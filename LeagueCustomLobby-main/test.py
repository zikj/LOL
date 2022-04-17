'''  1.执行cmd命令，不显示执行过程中弹出的黑框'''

def run_cmd(str="curl --version",echo_print=1):
    from subprocess import run
    if echo_print ==1:
        print('n\执行cmd命令="{}"'.format(str))
    run(str)





if __name__ == '__main__':
    run_cmd(str)
    '''run_cmd_Popen_fileno(str)'''

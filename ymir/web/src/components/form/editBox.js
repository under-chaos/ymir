import { useState, useEffect } from "react"
import { Modal, Form, Input } from "antd"
import t from '@/utils/t'
import { getTaskTypes } from '@/constants/query'

const { useForm } = Form
const EditBox = ({ children, record, dataType = 'task', action = () => { } }) => {
  const [editForm] = useForm()
  const [show, setShow] = useState(false)
  const { id, name, type, state } = record

  const types = getTaskTypes()

  useEffect(() => {
    // console.log('use effect: ', record)
    setShow(!!id)
    editForm.setFieldsValue({ name })
  }, [id])

  function onOk() {
    editForm.validateFields().then((values) => {
      const fname = values.name.trim()
      if (name === fname) {
        return
      }
      action(record, fname)
      setShow(false)
    })
  }
  function onCancel() {
    setShow(false)
    console.log('cancel id: ', record)
  }
  return <Modal
    visible={show}
    title={t('common.editbox.action.edit')}
    onCancel={onCancel}
    onOk={onOk}
    destroyOnClose
  >
    <Form form={editForm} labelCol={{ span: 6 }} colon={false} labelAlign='left'>
      <Form.Item
        label={t('common.editbox.name')}
        name='name'
        initialValue={name}
        rules={[
          { required: true, whitespace: true, message: t('common.editbox.form.name.required') },
          { type: 'string', min: 2, max: dataType === 'task' ? 20 : 30 },
        ]}
      >
        <Input placeholder={t('common.editbox.form.name.placeholder')} autoComplete={'off'} allowClear />
      </Form.Item>
      {children}
    </Form>
  </Modal>
}

export default EditBox

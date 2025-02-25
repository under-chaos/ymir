import {
  getHistory,
  getRuntimes,
  getStats,
} from "@/services/common"

export default {
  namespace: "common",
  state: {
  },
  effects: {
    *getHistory({ payload }, { call }) {
      const { code, result } = yield call(getHistory, payload)
      if (code === 0) {
        return result
      }
    },
    *getStats({payload}, { call }) {
      const { code, result } = yield call(getStats, payload)
      if (code === 0) {
        return result
      }
    },
    *getRuntimes({payload}, { call }) {
      const { code, result } = yield call(getRuntimes, payload)
      if (code === 0) {
        return result[0]
      }
    },
  },
  reducers: {
  },
}
